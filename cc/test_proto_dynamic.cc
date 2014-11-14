/* coding:utf-8
 * Copyright (C) dirlt
 */

#include <cassert>
#include <iostream>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/compiler/importer.h>
#include <google/protobuf/dynamic_message.h>
#include "sample.pb.h"

using namespace google::protobuf;
using namespace google::protobuf::compiler;
using namespace sample;

// ------------------------------------------------------------
// simplify usage of dynamic message in protobuf.
class ProtoDynamic:
    public google::protobuf::compiler::MultiFileErrorCollector {
public:
    ProtoDynamic(): importer_(&tree_, this) {
        tree_.MapPath("/", "/"); // absolute path.
        tree_.MapPath("", "."); // default starts with current directory.
    }
    void addMapPath(const char* vpath, const char* path) {
        tree_.MapPath(vpath, path);
    }
    virtual ~ProtoDynamic() {}
    struct ErrorMessage {
        std::string filename;
        int line;
        int column;
        std::string message;
    };
    std::vector< ErrorMessage > error_msg;
    virtual void AddError(const std::string& filename,
                          int line, int column,
                          const std::string& message) {
        ErrorMessage msg;
        msg.filename = filename;
        msg.line = line;
        msg.column = column;
        msg.message = message;
        error_msg.push_back(msg);
    }
    const google::protobuf::FileDescriptor* import(const std::string& filename) {
        return importer_.Import(filename);
    }
    static const google::protobuf::Descriptor* findMessageTypeByName(
        const google::protobuf::FileDescriptor* fd,
        const std::string& name) {
        return fd->pool()->FindMessageTypeByName(name);
    }
    static google::protobuf::MessageFactory* newMessageFactory(
        const google::protobuf::FileDescriptor* fd) {
        return new google::protobuf::DynamicMessageFactory(fd->pool());
    }
    static void deleteMessageFactory(google::protobuf::MessageFactory* factory) {
        delete factory;
    }
private:
    google::protobuf::compiler::DiskSourceTree tree_;
    google::protobuf::compiler::Importer importer_;
}; // class ProtoDynamic

int main() {
    std::string data;
    {
        // create message dynamicly.
        ProtoDynamic dynamic;
        const FileDescriptor* fd = dynamic.import("sample.proto");
        assert(fd);
        const Descriptor* desc = dynamic.findMessageTypeByName(fd, "sample.Session");
        assert(desc);
        MessageFactory* factory = dynamic.newMessageFactory(fd);
        Message* msg = factory->GetPrototype(desc)->New();
        const Reflection* reflection = msg->GetReflection();
        assert(reflection);

        reflection->SetString(msg, desc->FindFieldByName("user"), "dirlt");
        reflection->SetString(msg, desc->FindFieldByName("passwd"), "fuck");
        msg->SerializeToString(&data);
    }
    {
        Session session;
        session.ParseFromString(data);
        assert(strcmp(session.user().c_str(), "dirlt") == 0);
        assert(strcmp(session.passwd().c_str(), "fuck") == 0);
    }
    return 0;
}
